package main

import "net/http"
import "fmt"

type Message struct {
	Pid    byte
	Rtr    byte
	Length byte
	data   [8]byte
}

// SuccessQueryHandler manages all received logs from the PYNQ client
func SuccessQueryHandler(w http.ResponseWriter, req *http.Request) {
	fmt.Printf("Raw Data: %s\n", req.Body)
}
