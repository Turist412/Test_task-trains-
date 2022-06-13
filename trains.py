import pandas as pd


def time_gap(start_time_start, finish_time_start, finish_time_end=None):
    if finish_time_end is None:
        finish_time_end = start_time_start
    day = 24 * 60 * 60
    if finish_time_end <= start_time_start:
        gap1 = start_time_start - finish_time_end
    else:
        gap1 = day - finish_time_end + start_time_start
    if start_time_start <= finish_time_start:
        gap2 = finish_time_start - start_time_start
    else:
        gap2 = day - start_time_start + finish_time_start
    return gap1 + gap2


def min_time_find(start_platform, dataframe, not_visited, prev_time_finish=None):
    min_t = float("inf")
    min_i = -1
    min_platf = -1
    for start_time, finish_time, i, start_platf, end_platf in zip(dataframe.start_time_s, dataframe.finish_time_s, dataframe.index, dataframe.start_platform, dataframe.finish_platform):
        if start_platf == start_platform and end_platf in not_visited:
                if time_gap(start_time, finish_time,prev_time_finish) < min_t:
                    min_t = time_gap(start_time, finish_time,prev_time_finish)
                    min_i = i
                    min_platf = end_platf
    return min_t, min_i, min_platf


def find_path_by_time(frame, platforms, x):
    tmp_df = frame.copy()
    not_visited = platforms.copy()
    result_path = []
    result_time = 0
    min_time, index, finish = min_time_find(x, tmp_df, not_visited,None)
    result_time += min_time
    result_path.append(index)
    not_visited.remove(x)
    not_visited.remove(finish)
    next_to_find = finish
    while not_visited:
        fit_df = data.loc[(data["start_platform"] == next_to_find) & (data["finish_platform"].apply(lambda x: x in not_visited)),:]
        if fit_df.empty:
            print("Path not found")
            return result_path, result_time, 0
        last_time = data.loc[index]["finish_time_s"].max()
        min_time, index, finish = min_time_find(next_to_find, tmp_df, not_visited,last_time)
        result_time += min_time
        result_path.append(index)
        not_visited.remove(finish)
        next_to_find = finish
    return result_path, result_time, 1


def find_path_by_price(frame, platforms, x):
    tmp_df = frame.copy()
    not_visited = platforms.copy()
    result_path = []
    result_price = 0
    min_price = tmp_df.loc[(data["start_platform"] == x), :]["price"].min()
    result_price += min_price
    next_to_find = x
    index = data.loc[(data["start_platform"] == next_to_find) & (data["price"] == min_price)].index[0]
    result_path.append(index)
    finish = data.loc[(data["start_platform"] == next_to_find) & (data["price"] == min_price)]["finish_platform"].min()
    not_visited.remove(finish)
    not_visited.remove(x)
    next_to_find = finish
    while not_visited:

        fit_df = data.loc[
                 (data["start_platform"] == next_to_find) & (data["finish_platform"].apply(lambda x: x in not_visited)),
                 :]
        if fit_df.empty:
            return result_path, result_price, 0
        min_price = fit_df["price"].min()
        result_price += min_price
        index = data.loc[(data["start_platform"] == next_to_find) & (data["price"] == min_price)].index[0]
        result_path.append(index)
        finish = data.loc[(data["start_platform"] == next_to_find) & (data["price"] == min_price)]["finish_platform"].min()
        not_visited.remove(finish)
        next_to_find = finish
    return result_path, result_price, 1


data = pd.read_csv("C:/Users/Владелец/Downloads/test_task_data.csv", delimiter=";",
                   names=["start_platform", "finish_platform", "price", "start_time", "finish_time"], index_col=0)
data.drop_duplicates()
data["start_time_s"] = data["start_time"].apply(lambda x: int(x[:2]) * 3600 + int(x[3:5]) * 60 + int(x[7:9]))
data["finish_time_s"] = data["finish_time"].apply(lambda x: int(x[:2]) * 3600 + int(x[3:5]) * 60 + int(x[7:9]))
all_platforms = list(data["start_platform"].unique())

prices = []
pathes = []
pd.options.display.max_rows = 250
for x in all_platforms:
    path, price, res = find_path_by_price(data, all_platforms, x)
    if res:
        prices.append(price)
        pathes.append(path)

val = min(prices)
i = prices.index(val)
print("Best path :", *pathes[i])
print("Price of best path:", prices[i])
print()

times = []
pathes = []
for x in all_platforms:
    path, time_of_path, res = find_path_by_time(data, all_platforms, x)
    if res:
      times.append(time_of_path)
      pathes.append(path)

val = min(times)
i = times.index(val)
print("Best path :", *pathes[i])
print(f'Time of best path: {times[i]//3600}:{(times[i]%3600)//60}:{times[i]%3600 % 60}')
print()
