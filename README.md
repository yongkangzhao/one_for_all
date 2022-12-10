# one_for_all

environment setup requisite:
Maybe be run in one or more linux environment, developed using Ubuntu 22.
need anaconda, docker, make, nvidia-docker-toolbox, must also have GPU that's compatible with nvidia CUDA driver.

steps to run and utilize one for all:

1. install anaconda environment. use script in the utils directory.
```
source install_env.sh
```

2. deploy doccano, use script in the environment directory.
```
# optionally may want to rename .env.example to .env and make variable adjustment as needed
docker compose up -d
```

3. check if doccano is up.
```
go to localhost using browser and login with username and password defined in .env file
```

4. initialize some settings, use script in the environment directory.
```
python alter_tables.py
```

5. inside the generator directory, make changes to prompts and seeds as you see fit for your own generation purposes; or may use the default to see how it will be used.

6. deploy triple and sentence generator, under the top directory.
```
make build
make deploy

# use make destroy to stop the generators.
# edit the --host ip to where doccano is deployed.
```

7. as triples are being generated,  go to doccano and under the triple classification directory may begin to start labeling, and triple and sentence generator will use positive samples to make more generations. After a good amount of labels of both positive and negative that covers all entitie types, and prompts are done. may proceed to the next step.

8. train triple classifier, using script in classifier directory. first need to create dataset then train a model
```
# adjust ip to the doccano database if local use localhost
# adjust precision target is not super important here can be done at later step. adjust it as the quality of data and label changes.
python create_triple_dataset.py --host 54.183.139.246 --port 5432 --user postgres --password postgres --database postgres --dataset triple --output data
python train.py --model_name distilbert-base-uncased --epochs 10 --batch_size 8 --learning_rate 1e-5 --precision_target 0.99
```

9. after model is trained, we will need to tune the decision boundary of the model to make the predict of high precision, low recall is fine. this step is optional but highly recommened. 
```
python train.py --model_name distilbert-base-uncased --epochs 10 --batch_size 8 --learning_rate 1e-5 --precision_target 0.99 --train 0
```

10. finally we have model for automatically labeling of triples, we can run it with the following command
```
python label_triples.py 

                "
                -
                -
                h
                ost
                "
                ,
                "
                5
                4
                .
                1
                r3r
                r3r
                r2r
                r"r
                r
r
r
r
-


-


p


o
r
t 


"
rr

,
r
r
r
r
r
r
rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
                3
                2
                r,r
                r
r
r
r
r
r
r
r
r
r
s
e
r


"


,


" 


p


o
r
r
r
r
r
r
rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
                r"r
                r
r
r
r
r
r
r
r
p


a
s
s
w
o
r
d 


"


,
r
r
r
r
r
r
rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
                s
                t
                rrr
                r"r
                r
r
r
r
r
r
r
r
d


a
t
a
b
a
s
e 


"


,
r
r
r
r
r
r
rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
                s
                t
                rrr
                r"r
                r
r
r
r
r
r
r
r
m


o
d
e
l
_
n
a 
e


"


r
r
r
r
r
r
rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
                s
                t
                rlr
                rrr
                rbr
                rer
                rnr
                rsr
                d
                "
                ,
                

]


`
`
` 







rr
rr
rr
rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
