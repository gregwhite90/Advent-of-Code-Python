def update_group_questions(all_group_questions, group_questions):
    for part in ['one', 'two']:
        all_group_questions[f"part_{part}"].append(group_questions[f"part_{part}"])


def starting_g_q():
    return {
        'part_one': set(),
        'part_two': set(),
    }

def both_parts():
    all_group_questions = {
        'part_one': [],
        'part_two': [],
    }
    with open('input/input.txt') as input_file:
        group_questions = starting_g_q()
        rows_in_group = 0
        for row in input_file:
            if len(row.strip()) == 0:
                update_group_questions(all_group_questions, group_questions)
                group_questions = starting_g_q()
                rows_in_group = 0
            else:
                data = row.strip()
                questions = list(data)
                group_questions['part_one'].update(questions)
                # need to be smart for the first time
                if rows_in_group == 0:
                    group_questions['part_two'] = set(questions)
                else:
                    group_questions['part_two'] = group_questions['part_two'].intersection(set(questions))
                rows_in_group += 1
        # check last passport
        update_group_questions(all_group_questions, group_questions)
    return (
        sum([len(g_q) for g_q in all_group_questions['part_one']]),
        sum([len(g_q) for g_q in all_group_questions['part_two']]),        
    )

if __name__ == '__main__':
    print(both_parts())
