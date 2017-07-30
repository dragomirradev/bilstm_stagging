def read_sents(sents_file):
    stags = []
    with open(sents_file) as fhand:
        for line in fhand:
            stags_sent = line.split()
            stags.append(stags_sent)
    return stags
    
def output_conllu(sents_file, input_conllu_file, output_conllu_file):
    sent_idx = 0 
    word_idx = 0 
    stags = read_sents(sents_file)
    with open(output_conllu_file, 'wt') as fwrite:
        with open(input_conllu_file) as fhand:
            for line in fhand:
                tokens = line.split()
                if len(tokens) == 10: 
                    tokens.append(stags[sent_idx][word_idx])
                    word_idx += 1
                else:
                    sent_idx += 1
                    word_idx = 0 
                fwrite.write('\t'.join(tokens))
                fwrite.write('\n')

if __name__ == '__main__':
    sents_file = '/data/lily/jk964/Dropbox/dev.txt'
    input_conllu_file = '../../ud/stag_extraction/new_data/WSJ/conllu/wsj.dev.conllu1'
    output_conllu_file = 'wsj.dev.conllu_stag'
    output_conllu(sents_file, input_conllu_file, output_conllu_file)

