package main

import "net/http"

func main() {
	http.ListenAndServe("/message", log_handler.SuccessQueryHandler)
}
