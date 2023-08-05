package api

import (
    "github.com/gin-gonic/gin"
)


type API struct {
    config *config.Config
    router *gin.Engine
}

func NewAPI(config *config.Config) *API {
    api := &API {
        config: config,
        router: gin.Default(),
    }

    api.initRoutes()
    api.initMiddleware()

    return api
}


func (api *API) Run() {
    api.router.Run(":8080")
}

func (api *API) initRoutes() {

    api.router.GET("/crystals", api.getCrystalHandler)
    api.router.GET("/crystals", api.postCrystalHandler)
}

func (api *API) initMiddleware() {
    // TODO: add middleware
}
