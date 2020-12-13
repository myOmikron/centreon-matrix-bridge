adduser matrix
cp -r centreon_matrix /home/matrix
cp -r matrix_bridge /home/matrix
cp *.service /usr/lib/systemd/system
ln -s /usr/lib/systemd/system/centreon-listener.service /etc/systemd/system/multi-user.target.wants/
ln -s /usr/lib/systemd/system/matrix-handler.service /etc/systemd/system/multi-user.target.wants/
systemctl daemon-reload
systemctl enable centreon-listener.service
systemctl enable matrix-handler.service
cd /home/matrix && python3 -m venv venv
venv/bin/python -m pip install -U pip hopfenmatrix Django requests
