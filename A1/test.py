import pickle
lm_file = './data/lm_model.pkl'
with open(lm_file, 'rb') as fp:
    lm_model = pickle.load(fp)

lm_model.unk_prob = 1e-20
lm_model.set_mode('spell_check')

src_file = './data/output.txt'

with open(src_file, 'r') as fp:
    lines = [x.strip() for x in fp]
    for line in lines:
        print(lm_model.score(line))

# inp = None
# while (inp != '*'):
#     inp = input('Enter sentence: ')
#     print(lm_model.score(inp))
