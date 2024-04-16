import pytest

from p4_templates.kernel.create_depot import create_depot

class MockP4(object):
    def __init__(self, ):
        self.depot = {
            'Depot': 'Existing',
            'Type': 'stream',
            'StreamDepth': '//Existing/1'
        }

        self.fetch_called = 0
        self.save_called = 0

    def iterate_depots(self):
        return [self.depot]
    
    def fetch_depot(self, depot_name):
        self.depot['Depot'] = depot_name
        self.depot['StreamDepth'] = '//{}/1'.format(depot_name)
        self.fetch_called = 1
        return self.depot

    def save_depot(self, depot_spec):
        self.depot = depot_spec
        self.save_called = 1
        return self.depot
    

@pytest.mark.parametrize(
    'name,type,depth,dryrun,fetch_called,save_called,expected_depot',
    [
        ('test_depot','stream', 1, False, True, True, {'Depot': 'test_depot', 'Type': 'stream', 'StreamDepth': '//test_depot/1'}),
        ('Existing','stream', 1, False, False, False, {'Depot': 'Existing', 'Type': 'stream', 'StreamDepth': '//Existing/1'}),
        ('test_depot','stream', 1, True, True, False, {'Depot': 'test_depot', 'Type': 'stream', 'StreamDepth': '//test_depot/1'}),
    ]
)
def test_create_depot(name, type, depth, dryrun, fetch_called, save_called, expected_depot):
    m_server = MockP4()

    create_depot(m_server, name, type, depth, dryrun)
    
    assert m_server.depot == expected_depot
    assert m_server.fetch_called == fetch_called
    assert m_server.save_called == save_called
