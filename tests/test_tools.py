import hashlib,io,json,sys,tempfile,unittest,zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from validate import validate
from export_numeric import numeric
class ValidationTests(unittest.TestCase):
 def fixture(self,root,edge='0,1\n',name='pkg'):
  p=root/'fixture.zip'
  with zipfile.ZipFile(p,'w') as z:
   z.writestr('nodes.csv',f'id,name\n0,{name}\n1,other\n');z.writestr('edges.csv','source,target\n'+edge)
  item={'asset':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'node_rows':2,'edge_rows':1}
  (root/'catalog.json').write_text(json.dumps([item]));return root/'catalog.json'
 def test_valid(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);r=validate(p,self.fixture(p));self.assertEqual(r[0]['isolates'],0)
 def test_dangling(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)
   with self.assertRaises(AssertionError):validate(p,self.fixture(p,'0,2\n'))
 def test_email(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)
   with self.assertRaises(AssertionError):validate(p,self.fixture(p,name='test@example.invalid'))
 def test_numeric(self):self.assertEqual(numeric({'x':1,'path':'private','a':[2,'label']}),{'x':1,'a':[2]})
if __name__=='__main__':unittest.main()
