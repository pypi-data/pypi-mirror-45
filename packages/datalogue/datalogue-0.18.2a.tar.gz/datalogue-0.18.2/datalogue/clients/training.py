from typing import Optional, Union, List
from datalogue.clients.http import _HttpClient, HttpMethod
from datalogue.models.ontology import Ontology, OntologyNode, DataRef
from datalogue.errors import DtlError
from uuid import UUID

class _DataClient:
    """
    Client to interact with TrainingData
    """
    def __init__(self, http_client: _HttpClient):
        self.http_client = http_client

    def add(self, store_id: UUID, refs: List[DataRef]) -> Union[DtlError, List[UUID]]:
        """
        Attaches paths in the given `store_id` to the the nodes of the ontology.

        :param store_id: Id of the datatore that it going to be read
        :param refs: List of data references to show which paths are going to be attached which ontology nodes
        :return: List of stream ids which are the jobs that is transferring data from datastore to Themis
        """
        stream_ids = []
        dataset_id = self.__create_dataset()

        if isinstance(dataset_id, DtlError):
            return dataset_id

        for dataRef in refs:
            for path in dataRef.path_list:
                stream_id = self.__transfer_data_from_datastore(store_id, dataset_id, dataRef.node.name, path)
                self.__update_node(dataRef.node.node_id, path, dataset_id, stream_id)
                stream_ids.append(stream_id)
        return stream_ids

    def __create_dataset(self) -> Union[DtlError, UUID]:
        payload = {
            "title": "Sample Dataset",
            "tags": [],
            "label_map": {}
        }

        res = self.http_client.make_authed_request('/themis/dataset', HttpMethod.POST, body=payload)
        dataset_id = UUID(res.get("id"))

        if dataset_id is None:
            return DtlError("There is no dataset id in response!")
        return dataset_id

    def __transfer_data_from_datastore(self, store_id: UUID, dataset_id: UUID, node_label: str, path: List[str]) -> UUID:
        path_param = "&".join(map(lambda s: f"path={s}", path))
        url = f"/scout/run/training-data?sourceId={store_id}&{path_param}&trainingDataId={dataset_id}&class={node_label}"

        res = self.http_client.make_authed_request(url, HttpMethod.POST)

        stream_id = UUID(res["streamId"])
        return stream_id

    def __update_node(self, node_id: UUID, path: List[str], dataset_id: UUID, stream_id: UUID) -> None:
        #TODO We should remove this part when we move training data adding functionality out of Yggy
        entity_res = self.http_client.make_authed_request(f"/yggy/entity/{node_id}", HttpMethod.GET)
        training_data_list = entity_res.get("trainingDataInfo")
        if training_data_list is None:
            training_data_list = []

        training_data_list.append({
            "datasetId": str(dataset_id),
            "nodePath": path,
            "streamId": str(stream_id)
        })

        self.http_client.make_authed_request(f"/yggy/entity/{node_id}", HttpMethod.POST,
            body={"trainingDataInfo": training_data_list})
        

class _TrainingClient:
    """
    Client to interact with the Trainings
    """
    def __init__(self, http_client: _HttpClient):
        self.http_client = http_client
        self.data = _DataClient(http_client)

    #TODO API is not returning a training object, we should change this when the API returns training
    def run(self, ontology_id: UUID) -> Union[DtlError, bool]:
        """
        Starts training for a given ontology_id

        :param ontology_id:
        :return: Either a :class:`DtlError` if any error occurs or :class:`True` if training is requested successfully.
        """
        res = self.http_client.make_authed_request(f"/yggy/ontology/{ontology_id}/train", HttpMethod.POST)

        if isinstance(res, DtlError):
            return res

        return True