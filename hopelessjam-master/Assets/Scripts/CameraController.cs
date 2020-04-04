using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraController : MonoBehaviour
{

    public float minX, maxX, minY, maxY, speed;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKey(KeyCode.UpArrow)) {
            if (transform.position.y < maxY) {
                transform.Translate(new Vector2(0, speed * Time.deltaTime));
            }
        }
        if (Input.GetKey(KeyCode.DownArrow)) {
            if (transform.position.y > minY) {
                transform.Translate(new Vector2(0, -speed * Time.deltaTime));
            }
        }
        if (Input.GetKey(KeyCode.LeftArrow)) {
            if (transform.position.x > minX) {
                transform.Translate(new Vector2(-speed * Time.deltaTime, 0));
            }
        }
        if (Input.GetKey(KeyCode.RightArrow)) {
            if (transform.position.x < maxX) {
                transform.Translate(new Vector2(speed * Time.deltaTime, 0));
            }
        }
    }
}
