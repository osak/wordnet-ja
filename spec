require_relative 'wordnet'

ActiveRecord::Base.establish_connection(adapter: 'sqlite3', database: File.expand_path('~/app/wnjpn.db'))
describe Word do
  it "can be found" do
    word = Word.find_by(lemma: 'ルビー')
    word.should be_an_instance_of(Word)
    word.wordid.should == 187835
    word.lang.should == 'jpn'
    word.lemma.should == 'ルビー'
    word.pron.should be_nil
    word.pos.should == 'n'
  end

  it "has senses" do
    word = Word.find_by(lemma: 'ルビー')
    senses = word.senses
    senses.size.should == 2
  end
end

describe Sense do
  it "can be found" do
    sense = Sense.find_by(synset: '13372262-n', lang: 'jpn')
    sense.should be_an_instance_of(Sense)
    sense.synset.should == '13372262-n'
    sense.wordid.should == 187835
    sense.lang.should == 'jpn'
    sense.rank.should be_nil
    sense.lexid.should be_nil
    sense.freq.should be_nil
    sense.src.should == 'hand'

    sense = Sense.find_by(synset: '13372262-n', lang: 'eng')
    sense.should be_an_instance_of(Sense)
    sense.synset.should == '13372262-n'
    sense.wordid.should == 18004
    sense.lang.should == 'eng'
    sense.rank.should == 0
    sense.lexid.should == 1
    sense.freq.should == 1
    sense.src.should == 'eng-30'
  end

  it "has a word" do
    sense = Sense.find_by(synset: '13372262-n', lang: 'jpn')
    sense.word.should be_an_instance_of(Word)
    sense.word.wordid.should == 187835
  end

  it "has synsets" do
    sense = Sense.find_by(synset: '13372262-n', lang: 'jpn')
    sense.synsets.size.should == 1
  end
end

describe Synset do
  it "can be found" do
    synset = Synset.find_by(synset: '13372262-n')
    synset.should be_an_instance_of(Synset)
    synset.synset.should == '13372262-n'
    synset.pos.should == 'n'
    synset.name.should == 'ruby'
    synset.src.should == 'eng30'
  end

  it "has a sense" do
    synset = Synset.find_by(synset: '13372262-n')
    synset.senses.size.should == 2
  end

  it "has synset_defs" do
    synset = Synset.find_by(synset: '13372262-n')
    synset.synset_defs.size.should == 3
  end

  it "has ancestors" do
    synset = Synset.find_by(synset: '13372262-n')
    synset.ancestors.size.should == 9
    synset.ancestors.map{|a| a.hops}.should == (1..9).to_a
  end
end

describe SynsetDef do
  it "can be found" do
    synset_def = SynsetDef.find_by(synset: '13372262-n', lang: 'eng')
    synset_def.synset.should == '13372262-n'
    synset_def.lang.should == 'eng'
    synset_def.def.should == 'a transparent piece of ruby that has been cut and polished and is valued as a precious gem'
    synset_def.sid.should == 0
  end
end

describe Ancestor do
  it "can be found" do
    ancestor = Ancestor.find_by(synset1: '13372262-n', synset2: '03596787-n')
    ancestor.should be_an_instance_of(Ancestor)
    ancestor.synset1.should == '13372262-n'
    ancestor.synset2.should == '03596787-n'
    ancestor.hops.should == 1
  end
end
# vim:set ft=ruby:
