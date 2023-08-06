"""joyhong 개발용 모듈"""
def print_list(my_list):
    """리스트 안의 요소를 출력, 리스트 안의 요소가 리스트형일 경우에도 재귀호출로 요소를 출력한다."""
    for each_item in my_list:
        if isinstance(each_item, list):
            print_list(each_item)
        else:
            print(each_item)
