FROM odoo:13.0
#W'll use FROM karizma:13.0
USER root
RUN pip3 install --upgrade pip
RUN pip3 install xmltodict

USER odoo