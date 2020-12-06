adduser matrix
cp -r centreon_matrix /home/matrix
cp centreon-matrix.service /usr/lib/systemd/system/
ln -s /usr/lib/systemd/system/centreon-matrix.service /etc/systemd/system/multi-user.target.wants/
systemctl daemon-reload
systemctl enable centreon-matrix