import biom
import pandas as pd
import numpy as np
import tensorflow as tf
from skbio import OrdinationResults
from skbio.stats.composition import clr, clr_inv
from qiime2.plugin import Metadata
from rhapsody.multimodal import MMvec
from rhapsody.util import split_tables
from scipy.sparse import coo_matrix


def mmvec(microbes: biom.Table,
          metabolites: biom.Table,
          metadata: Metadata = None,
          training_column: str = None,
          num_testing_examples: int = 5,
          min_feature_count: int = 10,
          epochs: int = 100,
          batch_size: int = 50,
          latent_dim: int = 3,
          input_prior: float = 1,
          output_prior: float = 1,
          learning_rate: float = 0.001,
          summary_interval: int = 60) -> (pd.DataFrame, OrdinationResults):

    if metadata is not None:
        metadata = metadata.to_dataframe()

    # Note: there are a couple of biom -> pandas conversions taking
    # place here.  This is currently done on purpose, since we
    # haven't figured out how to handle sparse matrix multiplication
    # in the context of this algorithm.  That is a future consideration.
    res = split_tables(
        microbes, metabolites,
        metadata=metadata, training_column=training_column,
        num_test=num_testing_examples,
        min_samples=min_feature_count)

    (train_microbes_df, test_microbes_df,
     train_metabolites_df, test_metabolites_df) = res

    train_microbes_coo = coo_matrix(train_microbes_df.values)
    test_microbes_coo = coo_matrix(test_microbes_df.values)

    with tf.Graph().as_default(), tf.Session() as session:
        model = MMvec(
            latent_dim=latent_dim,
            u_scale=input_prior, v_scale=output_prior,
            learning_rate=learning_rate)
        model(session,
              train_microbes_coo, train_metabolites_df.values,
              test_microbes_coo, test_metabolites_df.values)

        loss, cv = model.fit(epoch=epochs, summary_interval=summary_interval)

        U, V = model.U, model.V

        U_ = np.hstack(
            (np.ones((model.U.shape[0], 1)),
             model.Ubias.reshape(-1, 1), U)
        )
        V_ = np.vstack(
            (model.Vbias.reshape(1, -1),
             np.ones((1, model.V.shape[1])), V)
        )

        microbe_embed = model.U
        metabolite_embed = np.hstack((np.zeros((V.shape[0], 1)), V)).T

        # make sure that the entries are row centered
        # only if the shape is greater than 1 (otherwise that will just
        # be subtracted out to zero.)
        if microbe_embed.shape[1] > 1:
            microbe_embed -= microbe_embed.mean(axis=1).reshape(-1, 1)
            metabolite_embed -= metabolite_embed.mean(axis=1).reshape(-1, 1)

        pc_ids = ['PC%d' % i for i in range(microbe_embed.shape[1])]
        features = pd.DataFrame(
            microbe_embed, columns=pc_ids,
            index=train_microbes_df.columns)
        samples = pd.DataFrame(
            metabolite_embed, columns=pc_ids,
            index=train_metabolites_df.columns)
        short_method_name = 'mmvec biplot'
        long_method_name = 'Multiomics mmvec biplot'
        eigvals = pd.Series(np.ones(len(pc_ids)), index=pc_ids)
        proportion_explained = pd.Series(np.ones(len(pc_ids)), index=pc_ids)
        biplot = OrdinationResults(
            short_method_name, long_method_name, eigvals,
            samples=samples, features=features,
            proportion_explained=proportion_explained)

        ranks = pd.DataFrame(
            clr(clr_inv(np.hstack(
                (np.zeros((model.U.shape[0], 1)), U_ @ V_)))),
            index=train_microbes_df.columns,
            columns=train_metabolites_df.columns)

        return ranks, biplot
