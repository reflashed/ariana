import csv
from nltk.corpus import verbnet

verbs = verbnet.lemmas()
transitive_verbs = []

for verb in verbs:
    class_ids = verbnet.classids(verb)

    for class_id in class_ids:
        vnclass = verbnet.vnclass(class_id)
        vnframes = vnclass.findall('FRAMES/FRAME')

        prettified_frames = verbnet.pprint_frames(class_id)
        is_transitive = 'Basic Transitive' in prettified_frames

        if is_transitive:
            transitive_verbs.append(verb)
            break

with open('verbs.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)

    for verb in transitive_verbs:
        writer.writerow([verb])
