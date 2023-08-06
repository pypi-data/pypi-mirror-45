echo "downloading drivers"
curl -SL https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip > chromedriver.zip && \
curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-37/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip && \
unzip headless-chromium.zip && \
unzip chromedriver.zip && \
rm headless-chromium.zip chromedriver.zip
echo "done"