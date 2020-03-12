def report():
    import pandas as pd
    from trust.models import Decision
    q = Decision.objects.filter(answer__isnull=False)
    df = pd.DataFrame(list(q.values('city__code', 'decision_type', 'owner__participant__code', 'answer')))
    table = pd.pivot_table(df, values='answer', index=['owner__participant__code'],
                           columns=['decision_type', 'city__code'])
    table.reset_index(inplace=True)
    table.columns = ['_'.join(col).strip() for col in table.columns.values]
    print(table.columns)
    table.to_csv(r'export_dataframe.csv', index=False, header=True)


if __name__ == '__main__' or __name__ == 'django.core.management.commands.shell':
    report()
