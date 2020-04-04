using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Trap : MonoBehaviour
{
    public GameController gamecontroller;
    public char trapChar;
    public float cooldownDuration, effectDuration;
    public Text trapText;
    public List<AudioClip> activationClips;
    public List<AudioClip> deathClips;
    public bool noRemainingUses = false;
    public GameObject deathAnimationPrefab;

    private bool isActive;
    private int remainingUses;
    private float lastUsedAt;
    private AudioSource sounds;

    void Start()
    {
        trapText = transform.GetChild(0).GetChild(0).GetComponent<Text>();
        remainingUses = 100;
        lastUsedAt = -999.9f;
        this.GetComponent<Animator>().Play("Idle");
        sounds = GetComponent<AudioSource>();
    }

    // Update is called once per frame
    void Update()
    {
        string timeUntilUse;
        if (lastUsedAt + cooldownDuration - Time.time > 0)
        {
            timeUntilUse = string.Format("{0:f2}", (lastUsedAt + cooldownDuration - Time.time));
        }
        else
        {
            timeUntilUse = "RDY";
        }
        trapText.text = string.Format("{0}", trapChar);
        if (Time.time - lastUsedAt > effectDuration)
        {
            isActive = false;
            this.GetComponent<Animator>().Play("Idle");
        }
    }

    public void TrapActivation()
    {
        if ((noRemainingUses || remainingUses > 0) && (Time.time - lastUsedAt > cooldownDuration))
        {
            if (activationClips.Count > 0)
            {
                sounds.PlayOneShot(activationClips[Random.Range(0, activationClips.Count)]);
            }
            isActive = true;
            remainingUses -= 1;
            lastUsedAt = Time.time;
            this.GetComponent<Animator>().Play("Kill");
        }
    }
    private void OnTriggerStay2D(Collider2D other)
    {
        if (isActive)
        {
            if (other.tag == "Human")
            {
                if (deathClips.Count > 0)
                {
                    sounds.PlayOneShot(deathClips[Random.Range(0, deathClips.Count)]);
                }
                if (deathAnimationPrefab != null)
                {
                    Instantiate(deathAnimationPrefab, other.gameObject.transform.position, Quaternion.identity);
                }
                gamecontroller.KillHuman(other.gameObject);
            }
        }
    }
}