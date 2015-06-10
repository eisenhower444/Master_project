----------------------------------------------------------------------
print '==> define parameters'

n_inputs  = 32*32
n_hidden  = 30

if opt.size == 'reduced' then
	n_outputs = 2
else
	n_outputs = 10
end

----------------------------------------------------------------------
print '==> construct model'

model = nn.Sequential()

model:add(nn.Linear(n_inputs, n_hidden))
model:add(nn.Sigmoid())
model:add(nn.Linear(n_hidden, n_outputs))
model:add(nn.SoftMax())

----------------------------------------------------------------------
print '==> here is the model:'
print(model)

----------------------------------------------------------------------
criterion = nn.ClassNLLCriterion()