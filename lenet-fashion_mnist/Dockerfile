FROM mindspore/mindspore-cpu:1.0.0

# setup the workspace
COPY . /workspace
WORKDIR /workspace

# fix: add to path
ENV PATH="/root/.local/bin:${PATH}"

# install the third-party requirements
RUN pip install --user -r requirements.txt

RUN python lenet.py --data_path ./MNIST_Data --device_target="CPU"

RUN python app.py -t index -n 1000

CMD ["python", "app.py", "-t", "query"]
