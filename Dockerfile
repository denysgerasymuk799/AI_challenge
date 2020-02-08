FROM python:3
ADD parser_work_ua.py /
ADD requirements.txt /
ADD work_ua_html_pages /
RUN pip install -r requirements.txt 
CMD [ "python", "./parser_work_ua.py" ]