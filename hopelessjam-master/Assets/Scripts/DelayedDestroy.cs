using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DelayedDestroy : MonoBehaviour
{
    public float delay;

    float endTime;

    private void Start()
    {
        endTime = Time.time + delay;
    }

    void Update()
    {
        if(Time.time > endTime)
        {
            Destroy(gameObject);
        }
    }
}
