docker run -it --network host daskdev/dask dask-scheduler  # start scheduler

docker run -it --network host daskdev/dask dask-worker localhost:8786 # start worker
docker run -it --network host daskdev/dask dask-worker localhost:8786 # start worker
docker run -it --network host daskdev/dask dask-worker localhost:8786 # start worker
docker run -it -e EXTRA_CONDA_PACKAGES="joblib" daskdev/dask dask-worker localhost:8786 # start specialized worker

docker run -it --network host daskdev/dask-notebook  # start Jupyter server
