----------------------------------------------------------------------
print '==> define parameters'

-- hidden units, filter sizes (for ConvNet only):
nfeaturemaps  = { {{ nfeaturemaps|join(', ') }} }
filtsize 	  = {{ filtsize }}
poolsize 	  = { {{ poolsize|join(', ') }} }
featuremaps_h = {{ featuremaps_h }}
featuremaps_w = {{ featuremaps_w }}
noutputs 	  = {{ noutputs }}

----------------------------------------------------------------------
print '==> construct model'
model = nn.Sequential()

-- stage 1 : mean suppresion -> filter bank -> squashing -> max pooling
model:add(cudnn.SpatialConvolution(nfeats, nfeaturemaps[1], filtsize, filtsize))
model:add(cudnn.{{ activation_function }}(true))
-- stage 2 : mean suppresion -> filter bank -> squashing 
model:add(cudnn.SpatialConvolution(nfeaturemaps[1], nfeaturemaps[2], filtsize, filtsize))
model:add(cudnn.{{ activation_function }}())
model:add(cudnn.SpatialMaxPooling(poolsize[1],poolsize[1],poolsize[1],poolsize[1]))
-- stage 3 : mean suppresion -> filter bank -> squashing -> max pooling
model:add(cudnn.SpatialConvolution(nfeaturemaps[2], nfeaturemaps[3], filtsize, filtsize))
model:add(cudnn.{{ activation_function }}())
-- stage 4 : mean suppresion -> filter bank -> squashing -> max pooling
model:add(cudnn.SpatialConvolution(nfeaturemaps[3], nfeaturemaps[4], filtsize, filtsize))
model:add(cudnn.{{ activation_function }}())
model:add(cudnn.SpatialMaxPooling(poolsize[2],poolsize[2],poolsize[2],poolsize[2]))
-- stage 5 : standard 2-layer MLP:
model:add(nn.View(nfeaturemaps[4]*featuremaps_h*featuremaps_w))
model:add(nn.Dropout(0.5))
model:add(nn.Linear(nfeaturemaps[4]*featuremaps_h*featuremaps_w, nfeaturemaps[5]))
model:add(nn.{{ activation_function }}())
model:add(nn.Dropout(0.5))
model:add(nn.Linear(nfeaturemaps[5], nfeaturemaps[6]))
model:add(nn.{{ activation_function }}())
-- model:add(nn.Tanh())
model:add(nn.Dropout(0.5))
model:add(nn.Linear(nfeaturemaps[6], noutputs))

model:add(nn.LogSoftMax())

-- 32*32 -> 28*28 -> 24*24 -> 12*12 -> 8*8 -> 4*4 -> 2*2 

----------------------------------------------------------------------
print '==> here is the model:'
print(model)