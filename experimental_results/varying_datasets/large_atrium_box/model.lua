----------------------------------------------------------------------
print '==> define parameters'

-- hidden units, filter sizes (for ConvNet only):
nfeaturemaps  = { 32, 64, 1000, 500 }
filtsize 	  = 5
poolsize 	  = { 2, 2 }
featuremaps_h = 5
featuremaps_w = 5
noutputs 	  = 2

----------------------------------------------------------------------
print '==> construct model'
model = nn.Sequential()

-- stage 1 : mean suppresion -> filter bank -> squashing -> max pooling
model:add(cudnn.SpatialConvolution(nfeats, nfeaturemaps[1], filtsize, filtsize))
model:add(cudnn.ReLU(true))
model:add(cudnn.SpatialMaxPooling(poolsize[1],poolsize[1],poolsize[1],poolsize[1]))
-- stage 2 : mean suppresion -> filter bank -> squashing -> max pooling
model:add(cudnn.SpatialConvolution(nfeaturemaps[1], nfeaturemaps[2], filtsize, filtsize))
model:add(cudnn.ReLU())
model:add(cudnn.SpatialMaxPooling(poolsize[2],poolsize[2],poolsize[2],poolsize[2]))
-- stage 3 : standard 2-layer MLP:
model:add(nn.View(nfeaturemaps[2]*featuremaps_h*featuremaps_w))
model:add(nn.Dropout(0.5))
model:add(nn.Linear(nfeaturemaps[2]*featuremaps_h*featuremaps_w, nfeaturemaps[3]))
model:add(nn.ReLU())
model:add(nn.Dropout(0.5))
model:add(nn.Linear(nfeaturemaps[3], nfeaturemaps[4]))
model:add(nn.ReLU())
-- model:add(nn.Tanh())
model:add(nn.Dropout(0.5))
model:add(nn.Linear(nfeaturemaps[4], noutputs))

model:add(nn.LogSoftMax())

----------------------------------------------------------------------
print '==> here is the model:'
print(model)

----------------------------------------------------------------------
criterion = nn.ClassNLLCriterion()