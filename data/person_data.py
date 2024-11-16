from fetch import DataFetch
import csv

fetch = DataFetch()


def main():
    datas = []
    try:
        with open('./person_new.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # 跳过标题行
            for row in reader:
                datas.append(row)
    except FileNotFoundError:
        pass

    n = len(datas)

    with open('./person_new.csv', 'w', newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        with open('./person.csv', 'r', encoding='utf-8') as filer:
            csv_reader = csv.reader(filer)
            next(csv_reader)  # 跳过标题行
            cnt = 0
            writer.writerow(['id', 'name', 'img', 'sex', 'birthday', 'birthplace', 'summary'])
            for row in csv_reader:
                pid, name, img, sex, birthday, birthplace, summary = row
                if cnt < n:
                    writer.writerow(datas[cnt])
                    cnt += 1
                    continue
                try:
                    data = fetch.get_info(name)
                    pid = data['pid']
                    birthday = data['birthday']
                    birthplace = data['birthplace']
                    summary = data['summary']
                except Exception as e:
                    pass

                row_data = [pid, name, img, sex, birthday, birthplace, summary]
                print(f"cnt = {cnt}: {row_data}")
                cnt += 1
                writer.writerow(row_data)

    print('Write csv file successfully')


if __name__ == '__main__':
    main()
