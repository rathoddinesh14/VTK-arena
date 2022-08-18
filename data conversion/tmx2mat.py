import dxchange

print(dxchange.__version__)

# apis
# print(dxchange.__builtins__)

# /Users/rathod_ias/Downloads/RCP_steel_tomo-A_recon.txm
data, metadata = dxchange.reader.read_txrm('/Users/rathod_ias/Downloads/RCP_steel_tomoA_recon.txm')

# print data shape
print(data.shape)
# type of data
print(type(data))

import scipy.io

# write to npy
# dxchange.writer.write_npy('/Users/rathod_ias/Downloads/RCP_steel_tomoA_recon.npy', data)
scipy.io.savemat('/Users/rathod_ias/Downloads/RCP_steel_tomoA_recon.mat', {'volm': data})

print(metadata)