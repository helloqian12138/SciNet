FROM gitpod/workspace-full

RUN sudo apt-get update  && sudo apt-get install -y rsync  && sudo rm -rf /var/lib/apt/lists/* && curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
RUN pip install --upgrade pip
RUN pip install matplotlib scikit-learn
RUN pip install -r requirements.txt
RUN pip install torch==1.7.1+cpu torchvision==0.8.2+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN export PATH=$PATH:~/.local/bin