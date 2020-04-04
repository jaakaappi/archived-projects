using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HumanController : MonoBehaviour {

    private Rigidbody2D rigidbody2d;
    private GameObject nextNode;
    private NodeController nextNodeController;

    private float distanceToFindNextNode = 0.2f;
    private float moveSpeed;

    private Vector2 target;
    

    // Start is called before the first frame update
    void Start() {
        rigidbody2d = GetComponent<Rigidbody2D>();
        SetNextNode(GameObject.FindGameObjectWithTag("StartNode"));
        moveSpeed = Random.Range(1f, 4f);
    }


    // Set tne next node where the human moves
    public void SetNextNode(GameObject newNode) {
        if (newNode != null) {
            nextNode = newNode;
            target = nextNode.transform.position;
            nextNodeController = (NodeController)nextNode.GetComponent(typeof(NodeController));
        } else {
            // If no next node, die
            Debug.Log("die");
            Destroy(gameObject);
        }
    }


    // Update is called once per frame
    void Update() {
        Vector2 direction = target - rigidbody2d.position;
        
        float distance = Vector2.Distance(rigidbody2d.position, target);

        if (distance >= distanceToFindNextNode) {
            // Move towards the next node
            direction.Normalize();
            rigidbody2d.MovePosition(rigidbody2d.position + moveSpeed * direction * Time.fixedDeltaTime);
        } else {
            // Node has been reached, get the next one
            SetNextNode(nextNodeController.GetNextNode());
        }
    }
}
