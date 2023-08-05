package api

import (
    "github.com/gin-gonic/gin"
)

func (api *API) getCrystalHandler(c *gin.Context) {

    //TODO: implement get logic
    crystals : = []model.Crystal{}
    c.JSON(200, crystals)
}
