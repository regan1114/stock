FROM centos

RUN yum -y update

RUN yum install -y \
  --setopt=tsflags=nodocs \
  --disableplugin=fastestmirror \
  openssh \
  openssh-server \
  sed \
  vim-minimal \
  zip \
  epel-release \
  python38 \
  && yum clean all \
  && rm -rf /var/cache/yum \
  && sed -e 's/#PermitRootLogin yes/PermitRootLogin yes/g' \
      -i /etc/ssh/sshd_config \
  && echo "root:password" | chpasswd \
  && systemctl enable sshd.service 

RUN yum install -y cronie && crond -V && \
    rm -rf /etc/cron.*/*

# WORKDIR python
COPY code ./

RUN pip3 install -r ./requirements.txt

COPY crontab /etc/cron.d/cjob

RUN chmod 0644 /etc/cron.d/cjob

CMD ["crond", "-n"]