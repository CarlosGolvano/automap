def print_header(header: str):
    line_len = 80
    mid_len_0 = (line_len - len(header) - 2) / 2
    mid_len_1 = mid_len_0 if mid_len_0.is_integer() else int(mid_len_0) + 1

    print('+' + '=' * (line_len - 2) + '+')
    print('+' + '=' * int(mid_len_0) + header + '=' * int(mid_len_1) + '+')
    print('+' + '=' * (line_len - 2) + '+')


def print_metrics(metrics: dict):
    # TODO: hardcoded metrics is bad.
    # metrics = ['tp', 'fp', 'fn', 'tn', 'precision', 'recall', 'f1']
    printable_metrics = ['p', 'r', 'f1']
    exclude = ["errors"]
    blanks = max(len(key) for key in metrics.keys()) + 1

    print(' ' * blanks + '\t'.join(printable_metrics))
    for key, values in metrics.items():
        if key not in exclude:
            print(key + ' ' * (blanks - len(key)), end="")
            for metric in printable_metrics:
                if metric in values:
                    if metric == printable_metrics[-1]:
                        print(f"{metrics[key][metric]:<.2f}", end="")
                    else:
                        print(f"{metrics[key][metric]:<.2f}\t", end="")
                else:
                    print(f"N/A\t", end="")
            print()


if __name__ == "__main__":
    import sys
    import json

    json_data = json.loads(sys.stdin.read())
    print_header("SUMMARY")
    print_metrics(json_data)
