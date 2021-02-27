def split_df(df):
    split_list = []
    for i in range(5):
        if i < 4:
            split_output = df[(df['rating'] >= i) & (df['rating'] < i + 1)]
        else:
            split_output = df[(df['rating'] >= i) & (df['rating'] <= float(i + 1))]
        split_list.append(split_output)
    return split_list