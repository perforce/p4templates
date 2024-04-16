import pytest

from p4_templates.kernel.create_branch import create_branch, populate_branch, delete_branch

class MockP4(object):
    def __init__(self, ):
        self.fetch_called = False
        self.save_called = False
        self.run_args = []
        self.delete_called = False
        self.branch = {
            'Branch': 'Existing',
            'Owner': None,
            'Options': None,
            'View': None
        }
    
    def fetch_branch(self, branch_name):
        self.branch['Branch'] = branch_name
        self.fetch_called = True
        return self.branch

    def save_branch(self, branch_spec):
        self.branch = branch_spec
        self.save_called = True
        return self.branch
    
    def delete_branch(self, branch_name):
        self.delete_called=True

    def run(self, *args):
        self.run_args = args
    


@pytest.mark.parametrize(
    'name,owner,options,view,dryrun,fetch_called,save_called,expected_branch',
    [
        ('test_branch','test_dude', ['options'], ['view'], False, True, True, {'Branch': 'test_branch','Options': 'options','Owner': 'test_dude','View': ['view']}),
        ('test_branch','test_dude', ['options'], {'view':'value'}, True, True, False, {'Branch': 'test_branch','Options': 'options','Owner': 'test_dude','View': ['view value']}),
    ]
)
def test_create_branch(name, owner, options, view, dryrun, fetch_called, save_called, expected_branch):
    m_server = MockP4()

    create_branch(m_server, name, owner, options, view, dryrun)
    
    assert m_server.fetch_called == fetch_called
    assert m_server.save_called == save_called
    assert m_server.branch == expected_branch

def test_populate_branch():
    m_server = MockP4()
    
    populate_branch(m_server, 'test_branch') 

    assert m_server.run_args == ('populate', '-b', 'test_branch')
    
def test_delete_branch():
    m_server = MockP4()

    delete_branch(m_server, 'test_branch')

    assert m_server.delete_called==True
