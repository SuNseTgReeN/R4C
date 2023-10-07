import os

import pandas as pd
from datetime import datetime, timedelta

from robots.models import RobotInfo


def robot_info_report():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    robot_info_data = RobotInfo.objects.filter(created__gte=start_date, created__lte=end_date)
    robot_info_dict = list(robot_info_data.values('model', 'version'))
    robot_info_df = pd.DataFrame.from_records(robot_info_dict)
    robot_info_counts = robot_info_df.groupby(['model', 'version']).size()
    data = []
    for model, version in robot_info_counts.index:
        count = robot_info_counts[(model, version)]
        data.append({
            'Модель': model,
            'Версия': version,
            'Количество за неделю': count
        })
    data_df = pd.DataFrame(data)
    current_directory = os.getcwd()
    report_directory = os.path.join(current_directory, 'report')
    if not os.path.exists(report_directory):
        os.makedirs(report_directory)
    save_path = os.path.join(report_directory, 'summary_report.xlsx')
    data_df.to_excel(save_path, sheet_name="Results", engine='xlsxwriter')
