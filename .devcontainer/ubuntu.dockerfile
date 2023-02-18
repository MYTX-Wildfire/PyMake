FROM ubuntu:jammy
USER root

ARG USERNAME=mythix
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG PYTHON_VERSION=3.11

# Install apt packages
RUN apt-get update -y && \
	apt-get install -y \
		git \
		python${PYTHON_VERSION} \
		python3-pip \
		ssh \
		sudo \
		vim && \
	update-alternatives --install \
		/usr/bin/python3 python3 /usr/bin/python${PYTHON_VERSION} 3

# Install pip packages
RUN python3 -m pip install \
	# Primary mkdocs package
	mkdocs \
	# Packages used to enable the material mkdocs theme
	mkdocs-material \
	mkdocs-git-revision-date-localized-plugin \
	pygments \
	# Packages for enabling plantuml support
	plantuml-markdown

# Create the user
RUN groupadd --gid $USER_GID $USERNAME && \
	useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash && \
	echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME && \
	chmod 0440 /etc/sudoers.d/$USERNAME
USER $USERNAME
