FROM python:3.9-slim
WORKDIR /app

RUN printf "deb [trusted=yes] https://mirror2.chabokan.net/debian bookworm main contrib non-free\n\
deb [trusted=yes] https://mirror2.chabokan.net/debian bookworm-updates main contrib non-free\n\
deb [trusted=yes] https://mirror2.chabokan.net/debian bookworm-security main contrib non-free\n" \
> /etc/apt/sources.list

RUN echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99ignore-valid-until && \
    echo 'Acquire::AllowInsecureRepositories "true";' >> /etc/apt/apt.conf.d/99ignore-valid-until && \
    echo 'Acquire::AllowDowngradeToInsecureRepositories "true";' >> /etc/apt/apt.conf.d/99ignore-valid-until && \
    echo 'APT::Get::AllowUnauthenticated "true";' >> /etc/apt/apt.conf.d/99ignore-valid-until

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libxcb-xinerama0 \
    libxcb-cursor0 \
    libxkbcommon-x11-0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-xfixes0 \
    libx11-xcb1 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

COPY mediapipe-0.8.6.2-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl /app

RUN pip config --user set global.index-url https://archive.ito.gov.ir/python/ && \
    pip config set global.extra-index-url https://pypi.jamko.ir/simple

RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir "numpy<1.24" "matplotlib<3.8" "protobuf<3.21"
RUN pip install --no-cache-dir \
    /app/mediapipe-0.8.6.2-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

COPY main.py .

CMD ["python", "/app/main.py"]
