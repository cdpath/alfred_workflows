package main

import (
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
)

type AlfredItem struct {
	Uid      string `json:"uid"`
	Type     string `json:"type,omitempty"`
	Title    string `json:"title"`
	Subtitle string `json:"subtitle"`
	Arg      string `json:"arg"`
	Icon     string `json:"icon"`
}

type AlfredItems struct {
	Items []AlfredItem `json:"items"`
}

type ProfilesResp struct {
	Profiles []string `json:"profiles"`
}

type SwitchProfilePayload struct {
	Name string `json:"name"`
}

func sendListProfiles() string {
	client := &http.Client{}
	req, err := http.NewRequest("GET", "http://localhost:6171/v1/profiles?sensitive=0", nil)
	req.Header.Add("X-Key", os.Getenv("XKEY"))

	parseFormErr := req.ParseForm()
	if parseFormErr != nil {
		fmt.Println(parseFormErr)
	}

	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Failure : ", err)
	}

	respBody, _ := ioutil.ReadAll(resp.Body)

	profiles := ProfilesResp{}
	jsonErr := json.Unmarshal(respBody, &profiles)
	if jsonErr != nil {
		log.Fatal(jsonErr)
	}

	var Items []AlfredItem

	for key, profile := range profiles.Profiles {
		if profile == "Default" {
			continue
		}
		Item := AlfredItem{
			Uid:      string(key),
			Type:     "default",
			Title:    "Profile: " + profile,
			Subtitle: "Switch profile",
			Arg:      profile,
			Icon:     "icon.png",
		}
		Items = append(Items, Item)
	}

	output := &AlfredItems{
		Items: Items,
	}
	output_str, _ := json.Marshal(output)
	return string(output_str)
}

func sendSwitchProfiles(profile string) {
	payload := &SwitchProfilePayload{
		Name: profile,
	}
	payload_str, _ := json.Marshal(payload)
	body := bytes.NewBuffer(payload_str)

	client := &http.Client{}
	req, err := http.NewRequest("POST", "http://localhost:6171/v1/profiles/switch", body)
	req.Header.Add("X-Key", os.Getenv("XKEY"))
	parseFormErr := req.ParseForm()
	if parseFormErr != nil {
		fmt.Println(parseFormErr)
	}
	resp, err := client.Do(req)

	if err != nil {
		fmt.Println("Failure : ", err)
	}

	if resp.StatusCode >= 200 && resp.StatusCode <= 299 {
		fmt.Println(profile)
	}
}

func main() {
	actionPtr := flag.String("a", "list", "action to take")
	profilePtr := flag.String("p", "focus", "profile to choose")
	flag.Parse()

	action := *actionPtr
	profile := *profilePtr

	if action == "list" {
		output := sendListProfiles()
		fmt.Println(output)
	} else if action == "switch" && len(profile) > 0 {
		sendSwitchProfiles(profile)
	}

}
