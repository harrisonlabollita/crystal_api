package main

import (
        "github.com/harrisonlabollita/crystal_api/api"
        "github.com/harrisonlabollita/crystal_api/config"
)

func main() {

    cfg := config.LoadConfig()

    apiServer := api.NewAPI(cfg)
    apiServer.Run()
}
