module Page.Home exposing (Model, Msg(..), init, update, view)

import Data.Activite as Activite exposing (Activite)
import Data.Commune as Commune exposing (Commune)
import Data.Erp as Erp exposing (Erp)
import Data.Session exposing (Session)
import Html exposing (..)
import Html.Attributes exposing (..)
import Http
import Markdown
import Request.Activite
import Request.Erp
import Route exposing (Route)


type alias Model =
    { commune : Maybe Commune
    , activiteSlug : Maybe Activite.Slug
    , erpSlug : Maybe Erp.Slug
    , activites : List Activite
    , erps : List Erp
    }


type Msg
    = ActivitesReceived (Result Http.Error (List Activite))
    | ErpsReceived (Result Http.Error (List Erp))
    | NoOp


init : Session -> Route -> ( Model, Session, Cmd Msg )
init session route =
    let
        base =
            { commune = Nothing
            , activiteSlug = Nothing
            , erpSlug = Nothing
            , activites = session.activites
            , erps = session.erps
            }

        model =
            case route of
                Route.Home ->
                    base

                Route.CommuneHome commune ->
                    { base | commune = Just commune }

                Route.Activite activiteSlug ->
                    { base | activiteSlug = Just activiteSlug }

                Route.Erp erpSlug ->
                    { base | erpSlug = Just erpSlug }

                Route.CommuneActivite commune activiteSlug ->
                    { base
                        | commune = Just commune
                        , activiteSlug = Just activiteSlug
                    }

                Route.CommuneActiviteErp commune activiteSlug erpSlug ->
                    { base
                        | commune = Just commune
                        , activiteSlug = Just activiteSlug
                        , erpSlug = Just erpSlug
                    }

                Route.CommuneErp commune erpSlug ->
                    { base
                        | commune = Just commune
                        , erpSlug = Just erpSlug
                    }
    in
    ( model
    , { session
        | commune = model.commune
        , activites = model.activites
        , erps = model.erps
      }
    , Cmd.batch
        [ Request.Activite.list session model.commune ActivitesReceived
        , Request.Erp.list session model.commune model.activiteSlug Nothing ErpsReceived
        ]
    )


update : Session -> Msg -> Model -> ( Model, Session, Cmd Msg )
update session msg model =
    case msg of
        ActivitesReceived (Ok activites) ->
            ( { model | activites = activites }, session, Cmd.none )

        ActivitesReceived (Err error) ->
            ( model, session, Cmd.none )

        ErpsReceived (Ok erps) ->
            ( { model | erps = erps }, session, Cmd.none )

        ErpsReceived (Err error) ->
            let
                _ =
                    Debug.log "error erp" error
            in
            ( model, session, Cmd.none )

        NoOp ->
            ( model
            , session
            , Cmd.none
            )


activitesListView : Model -> Html Msg
activitesListView model =
    model.activites
        |> List.map
            (\activite ->
                a
                    [ class "list-group-item list-group-item-action d-flex justify-content-between align-items-center"
                    , case model.commune of
                        Just commune ->
                            Route.href (Route.CommuneActivite commune activite.slug)

                        Nothing ->
                            Route.href (Route.Activite activite.slug)
                    ]
                    [ text activite.nom
                    , case activite.count of
                        Just count ->
                            span [ class "badge badge-primary badge-pill" ] [ text (String.fromInt count) ]

                        Nothing ->
                            text ""
                    ]
            )
        |> div [ class "list-group list-group-flush border-right" ]


erpListEntryView : Model -> Erp -> Html Msg
erpListEntryView model erp =
    a
        [ class "list-group-item list-group-item-action d-flex justify-content-between align-items-center a4a-erp-list-item"
        , case model.commune of
            Just commune ->
                Route.href (Route.CommuneErp commune erp.slug)

            Nothing ->
                Route.href (Route.Erp erp.slug)
        ]
        [ span [ class "flex-fill" ]
            [ text erp.nom
            , br [] []
            , small [ class "text-muted" ]
                [ case erp.activite of
                    Just activite ->
                        span [] [ strong [] [ text activite.nom ], text " » " ]

                    Nothing ->
                        text ""
                , text erp.adresse
                ]
            ]
        , if erp.hasAccessibilite then
            button
                [ class "btn btn-sm btn-outline-success mr-2 a4a-icon-btn"
                , title "Les informations d'accessibilité sont disponibles"
                ]
                [ i [ class "icon icon-checklist" ] []
                , span [ class "sr-only" ]
                    [ text "Les informations d'accessibilités sont disponibles" ]
                ]

          else
            text ""
        , button
            [ class "btn btn-sm btn-outline-primary d-none d-sm-none d-md-block a4a-icon-btn a4a-geo-link"
            , attribute "data-erp-id" "11571"
            , title "Localiser sur la carte"
            ]
            [ i [ class "icon icon-target" ] []
            ]
        ]


view : Session -> Model -> ( String, List (Html Msg) )
view _ model =
    ( case model.commune of
        Just commune ->
            commune.nom

        Nothing ->
            "Accueil"
    , [ div [ class "container-fluid p-0 m-0 a4a-app-content" ]
            [ header [ class "a4a-app-title row p-0 m-0" ]
                [ div [ class "col pt-2 pb-1" ]
                    [ h2 [ class "display-4", id "content", attribute "style" "font-size:32px" ]
                        [ case model.commune of
                            Just commune ->
                                span []
                                    [ text "Commune de "
                                    , a [ Route.href (Route.CommuneHome commune) ] [ text commune.nom ]
                                    ]

                            Nothing ->
                                text "Toutes les communes"
                        , case model.activiteSlug of
                            Just activiteSlug ->
                                small [ class "text-muted" ]
                                    [ text " » "

                                    -- TODO: link to activite
                                    , model.activites
                                        |> Activite.findBySlug activiteSlug
                                        |> Debug.log ""
                                        |> Maybe.map .nom
                                        |> Maybe.withDefault ""
                                        |> text
                                    ]

                            Nothing ->
                                text ""
                        ]
                    ]
                ]
            , div [ class "row p-0 m-0" ]
                [ nav
                    [ class "a4a-app-nav col-lg-2 col-md-3 col-sm-4 d-none d-sm-block bg-light activites-list p-0 m-0 border-top overflow-auto"
                    , attribute "role" "navigation"
                    ]
                    [ h3 [ class "sr-only" ]
                        [ text "Liste des domaines d'activité" ]
                    , activitesListView model
                    ]
                , main_ [ class "a4a-app-main col-lg-5 col-md-5 col-sm-8 erp-list p-0 m-0 border-top overflow-auto" ]
                    [ model.erps
                        |> List.map (\erp -> erpListEntryView model erp)
                        |> div [ class "list-group list-group-flush" ]
                    ]
                , div [ class "a4a-app-map col-lg-5 col-md-4 d-none d-md-block map-area p-0 m-0" ]
                    [ div [ class "a4a-map", id "map" ]
                        []
                    ]
                ]
            ]
      ]
    )