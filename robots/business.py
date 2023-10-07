import os
from datetime import datetime, timedelta
import pandas as pd
import xlsxwriter

from robots.models import RobotInfo


def robot_info_report():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    robot_info_data = RobotInfo.objects.filter(created__gte=start_date, created__lte=end_date)
    robot_info_dict = list(robot_info_data.values('model', 'version'))
    robot_info_df = pd.DataFrame.from_records(robot_info_dict)
    robot_info_counts = robot_info_df.groupby(['model', 'version']).size()
    current_directory = os.getcwd()
    report_directory = os.path.join(current_directory, 'report')
    if not os.path.exists(report_directory):
        os.makedirs(report_directory)
    save_path = os.path.join(report_directory, 'summary_report.xlsx')
    workbook = xlsxwriter.Workbook(save_path)
    header_format = workbook.add_format({'bold': True})
    model_versions = {}
    for model, version in robot_info_counts.index:
        if model not in model_versions:
            model_versions[model] = []
        model_versions[model].append(version)
    for model, versions in model_versions.items():
        worksheet = workbook.add_worksheet(model)

        worksheet.write(0, 0, 'Модель', header_format)
        worksheet.write(0, 1, 'Версия', header_format)
        worksheet.write(0, 2, 'Количество за неделю', header_format)
        row = 1
        for version in versions:
            count = robot_info_counts[(model, version)]
            worksheet.write(row, 0, model)
            worksheet.write(row, 1, version)
            worksheet.write(row, 2, count)
            row += 1

    workbook.close()
