# AWS deployment

These are the notes to set up automatic generation of updated figures in serverless way.

## Lambda

* For creating custom lambda layer that has pandas and altair:

```bash
cd lambda
docker run -v "$PWD":/var/task "lambci/lambda:build-python3.7" /bin/sh -c "pip install -r requirements.txt -t python/lib/python3.7/site-packages/; exit"
zip -r python-layer.zip python > /dev/null
```
The zip file is uploaded to AWS via console, and used as layer.

* Files `utils.py` and `app.py` are uploaded as function code.
* Runtime has `Python 3.7` and `lambda_function.lambda_handler` configured.
* Basic settings include `128 MB` memory and `30 sec`timeout.


## SNS
* A topic is created, so that e-mail notifications can be sent when errors occur. Errors are captured in Cloudwatch.

## Cloudwatch

* Events/Rules is configured to execute the Lambda function every two minutes. Following Cron expression is used: `0/2 * * * ? *`
* Alarm is configured to monitor Lambda function outcomes. Statistic is `Maximum` of `Error` with `1 minute` period. Threshold of `Greater than 0` is deployed.

