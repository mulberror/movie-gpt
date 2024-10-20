from fetch import DataFetch
import json

if __name__ == '__main__':
    fetch = DataFetch()
    result = fetch.get_info('贾康熙')
    for i, j in result.items():
        print(i, ':', j)