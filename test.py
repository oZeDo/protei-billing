# import itertools
#
# # Значения параметров
# values = ["correct", "incorrect", "empty"]
#
# # Словарь параметров с их типом
# params = {
#     "msisdn": {
#         "type": "OM",
#     },
#     "imsi": {
#         "type": "OM",
#     },
#     "limit": {
#         "type": "M",
#     },
#     "enable_notification": {
#         "type": "O",
#     }
# }
# param_list = list(params.keys())
# service_name = "enable_money_counter_"  # Название тестируемого сервиса
#
# # Все возможные комбинации значений для данных параметров
# combinations = list(itertools.product([x for x in range(len(values))], repeat=len(param_list)))
# for test_num, combination in enumerate(combinations):
#     test_name = "test_"
#     test = {}
#     # Значение параметров в данном тесте
#     for param_index, param_name in enumerate(param_list):
#         test.update({param_name: values[combination[param_index]]})
#
#     # Анализ удачен ли тест будет или нет, по заданным типам параметров (Mandatory, Optional, OptionalMandatory)
#     # OptionalMandatory = 2 или более параметра опциональны, но один из них обязательно должен быть
#     # !TODO: Анализ тестов по типам параметрам
#     # !TODO: Откинуть бессмысленные тесты
#     # if test[param_list[0]] == "incorrect" or test[param_list[1]] == "incorrect":
#     #     test_name += "unable_to_"
#     # elif test[param_list[2]] == "incorrect" or test[param_list[2]] == "empty":
#     #     test_name += "unable_to_"
#     # elif test[param_list[3]] == "incorrect":
#     #     test_name += "unable_to_"
#     test_name += service_name
#
#     # Собрать название теста
#     for param_name in param_list:
#         test_name += f"with_{test[param_name]}_{param_name}_"  # example: with_{incorrect}_{imsi}_
#     test_name = test_name[:-1]  # убрать _ в конце
#
#     print(test_num, test_name)

