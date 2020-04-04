using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NodeController : MonoBehaviour {

    public GameObject[] nextNodes;


    // Return a random node from the nextNodes list
    public GameObject GetNextNode() {
        if (nextNodes != null && nextNodes.Length > 0) {
            int random = Random.Range(0, nextNodes.Length);
            return nextNodes[random];
        } else {
            return null;
        }
    }
}
