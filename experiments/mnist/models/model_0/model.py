import torch
import torch.nn as nn
import numpy


class Create(torch.nn.Module):

    def __init__(self, input_shape, output_shape):
        super(Create, self).__init__()

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        fc_size         = numpy.prod(input_shape)
        classes_count   = numpy.prod(output_shape)

        self.layers = [ 
                        nn.Flatten(),

                        nn.Linear(fc_size, 128),
                        nn.ReLU(),

                        nn.Linear(128, classes_count)
        ]
     
        for i in range(len(self.layers)):
            if hasattr(self.layers[i], "weight"):
                torch.nn.init.xavier_uniform_(self.layers[i].weight)

        self.model = nn.Sequential(*self.layers)
        self.model.to(self.device)

        print(self.model)

    def forward(self, x):
        return self.model.forward(x)
    
    def save(self, path):
        name = path + "model.pt"
        print("saving", name)
        torch.save(self.model.state_dict(), name) 

    def load(self, path):
        name = path + "model.pt"
        print("loading", name)

        self.model.load_state_dict(torch.load(name, map_location = self.device))
        self.model.eval() 