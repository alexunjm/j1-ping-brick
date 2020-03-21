# pygame env

## comandos

solo para crearlo la primera vez

`conda create -n myenv python=3.6`

cada vez que se vaya a trabajar en éste ambiente, activarlo antes

`conda activate myenv`

para ver los ambientes y cual está activo

`conda info --envs`


para instalar pygame

`python3 -m pip install -U pygame --user`

para probar que haya quedado instalado pygame

`python3 -m pygame.examples.aliens`