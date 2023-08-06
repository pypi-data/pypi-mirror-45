from mhclovac import *
from proteinko import Proteinko
import os
import numpy as np
import pickle


def fasta_reader(fasta_path):
    with open(fasta_path, 'r') as f:
        seq_name = ''
        sequence = ''
        write_flag = 0
        for line in f:
            if line.startswith('>'):
                if write_flag:
                    write_flag = 0
                    yield(seq_name, sequence)
                seq_name = line.split()[0][1:]
                sequence = ''
            else:
                sequence += line.strip()
                write_flag = 1
        yield (seq_name, sequence)


def load_models():
    current_dir = os.path.dirname(__file__)
    models_file = '/'.join([current_dir, 'trained_models'])
    with open(models_file, 'rb') as f:
        return pickle.load(f)


def get_feature_vector(seq, normed_dist=True, normed_auc=True):
    """
    Get feature vector for protein sequence.
    :param seq: string sequence
    :param sckeys: string property schema key
    :return:
    """
    prt = Proteinko()
    norm_range_options = {
        'hydropathy': (-1, 1),
        'acceptors': (0, 1),
        'donors': (0, 1),
        'pI': (-1, 1),
        'volume': (-1, 1)
    }
    property_schemas = ['hydropathy', 'acceptors', 'donors', 'pI', 'volume']
    auc_window = 10
    auc_step = 5
    vlen = 100
    auc_dict = {}
    for sc in property_schemas:
        s = prt.get_dist(
            sequence=seq,
            schema=sc,
            vlen=vlen,
            norm_range=norm_range_options[sc],
            normed=normed_dist
        )
        auc = rolling_auc(
            s=s,
            window=auc_window,
            step=auc_step,
            normalize=normed_auc
        )
        auc_dict[sc] = auc
    feature_vec = flatten_features(auc_dict, property_schemas)
    return feature_vec.reshape(1, -1)


def rolling_auc(s, step=5, window=10, normalize=False):
    auc_array = list()
    nsteps = ((len(s) - window) // step) + 1
    for i in range(nsteps):
        offset = i * step
        end = offset + window
        auc = np.trapz(s[offset:end])
        auc_array.append(auc)
    # Cast list to numpy array
    auc_array = np.array(auc_array)
    if normalize:
        # Normalize values to range 0 - 1
        auc_array = (auc_array-auc_array.min())/(auc_array.max()-auc_array.min())
    return auc_array


def flatten_features(row, keys, normalize=False):
    result = []
    for sc in keys:
        result.extend(row[sc])
    result = np.array(result)
    if normalize:
        result = (result-result.min())/(result.max()-result.min())
    return result


def print_header(output):
    line = '\t'.join(['seq_name', 'hla', 'peptide', 'ic50'])
    output.write(line + '\n')
    return
