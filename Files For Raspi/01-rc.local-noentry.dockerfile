# syntax=docker/dockerfile:1

FROM lfp_tmpl00:latest

WORKDIR /src
# Copy necessary files into container image
ADD ["register_recorder.py", "."]
ADD ["setup.sh", "."]
ADD ["Penetrometer_execution_code.py", "."]

# create rc.local and set the executable bit
RUN touch /etc/rc.local
RUN chmod +x /etc/rc.local
# Set executable bit for the setup script
RUN chmod +x setup.sh

CMD /bin/bash
