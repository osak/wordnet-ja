require 'active_record'

def define_wn_relation(rel)
  define_method("wn_" + rel.to_s) { |name, keyname, *args|
    opt = {primary_key: keyname, foreign_key: keyname}
    opt.merge!(args.first) if args.first.is_a?(Hash)
    __send__(rel, name, opt)
  }
end

define_wn_relation :has_one
define_wn_relation :has_many
define_wn_relation :belongs_to

class Word < ActiveRecord::Base
  self.table_name = 'word'
  composed_of :wordid , class_name: Integer.to_s
  composed_of :lang   , class_name: String.to_s
  composed_of :lemma  , class_name: String.to_s
  composed_of :pron   , class_name: String.to_s
  composed_of :pos    , class_name: String.to_s

  wn_has_many :senses, :wordid
end

class Sense < ActiveRecord::Base
  self.table_name = 'sense'
  attr_accessor :synset, :wordid, :lang, :rank, :lexid, :freq, :src
  wn_belongs_to :word, :wordid
  wn_has_many :synsets, :synset
end

class Synset < ActiveRecord::Base
  self.table_name = 'synset'
  composed_of :synset , class_name: String.to_s
  composed_of :pos    , class_name: String.to_s
  composed_of :name   , class_name: String.to_s
  composed_of :text   , class_name: String.to_s

  wn_belongs_to :sense, :synset
  wn_has_one :synset_def, :synset, class_name: 'SynsetDef'
  has_many :ancestors, primary_key: :synset, foreign_key: :synset1, order: :hops
end

class SynsetDef < ActiveRecord::Base
  self.table_name = 'synset_def'
  composed_of :synset , class_name: String.to_s
  composed_of :lang   , class_name: String.to_s
  composed_of :def    , class_name: String.to_s
  composed_of :sid    , class_name: String.to_s

  wn_belongs_to :synset, :synset
end

class Ancestor < ActiveRecord::Base
  self.table_name = 'ancestor'
  composed_of :synset1 , class_name: String.to_s
  composed_of :synset2 , class_name: String.to_s
  composed_of :hops    , class_name: Integer.to_s
end
