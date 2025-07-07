<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0">
    <xsl:output method="html"/>
    
    <xsl:template match="/">
        <html>
            <head>
                <title><xsl:value-of select="/tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title[@type='main']"/></title>
                <link rel="stylesheet" type="text/css" href="style.css"/>
            </head>
            <body>
                <div class="page-box">
                    <xsl:apply-templates select="tei:TEI/tei:text/tei:front/tei:titlePage"/>
                </div>
                <xsl:apply-templates select="tei:TEI/tei:text/tei:body"/>
            </body>
        </html>
    </xsl:template>

    <!-- template for front page -->
    <xsl:template match="tei:front/tei:titlePage">
        <div class="front-page">
            <!-- main Title -->
            <div class="title-main">
                <xsl:for-each select="tei:docTitle/tei:titlePart[@type='main']/tei:title">
                    <p class="title-main-line n{@n}">
                        <xsl:apply-templates/>
                    </p>
                </xsl:for-each>
            </div>

            <!-- subtitle -->
            <div class="title-sub">
                <xsl:for-each select="tei:docTitle/tei:titlePart[@type='sub']/tei:title">
                    <p class="title-sub-line n{@n}">
                        <xsl:apply-templates/>
                    </p>
                </xsl:for-each>
            </div>

            <!-- descriptive title -->
            <div class="title-desc">
                <xsl:value-of select="tei:docTitle/tei:titlePart[@type='desc']/tei:title"/>
            </div>

            <!-- figure -->
            <xsl:apply-templates select="tei:figure"/>

            <!-- epigraph -->
            <xsl:apply-templates select="tei:epigraph"/>

            <!-- note -->
            <div class="note-wrapper">
                <hr/>
                    <p class="note">
                        <xsl:value-of select="tei:note[@type='contents']"/>
                    </p>
                <hr/>
            </div>

            <!-- publication info -->
            <xsl:apply-templates select="tei:docImprint"/>
        </div>
    </xsl:template>

    <!-- fig with graphic -->
    <xsl:template match="tei:figure">
        <div>
            <xsl:apply-templates select="tei:graphic"/>
        </div>
    </xsl:template>

    <xsl:template match="tei:graphic">
        <img>
            <xsl:attribute name="src">
                <xsl:value-of select="@url"/>
            </xsl:attribute>
            <xsl:attribute name="alt">new-england-witch</xsl:attribute>
        </img>
    </xsl:template>

    <!-- epigraph -->
    <xsl:template match="tei:epigraph">
    <div class="epigraph">
        <xsl:for-each select="tei:cit/tei:quote/tei:l">
        <p>
            <xsl:attribute name="class">
            <xsl:choose>
                <xsl:when test="position()=1">first-line</xsl:when>
                <xsl:when test="position()=last()">last-line</xsl:when>
                <xsl:otherwise>middle-line</xsl:otherwise>
            </xsl:choose>
            </xsl:attribute>
            <xsl:value-of select="."/>
        </p>
        </xsl:for-each>
        <xsl:if test="tei:cit/tei:bibl">
        <div class="bibl">
            <xsl:value-of select="tei:cit/tei:bibl"/>
        </div>
        </xsl:if>
    </div>
    </xsl:template>

    <!-- docImprint -->
    <xsl:template match="tei:docImprint">
        <div class="docImprint">
            <p><xsl:apply-templates select="tei:pubPlace"/></p>
            <p><xsl:apply-templates select="tei:publisher"/></p>
            <p><xsl:apply-templates select="tei:docDate"/></p>
        </div>
    </xsl:template>

    <!-- body -->
    <xsl:template match="tei:body">
        <div>
            <xsl:apply-templates select="tei:div"/>
        </div>
    </xsl:template>

    <!-- page div -->
    <xsl:template match="tei:div">
        <xsl:apply-templates select="tei:pb"/>
        <div class="page-header">
            <xsl:apply-templates select="tei:fw[@rend='left']"/>
            <xsl:apply-templates select="tei:fw[@rend='center']"/>
        </div>
        <xsl:apply-templates select="tei:head"/>
        <xsl:apply-templates select="tei:p"/>
    </xsl:template>


    <xsl:template match="tei:head">
        <div class="titlePage">
            <xsl:value-of select="."/>
        </div>
    </xsl:template>

    <xsl:template match="tei:pb">
        <hr class="page-divider"/>    
    </xsl:template>

    <!-- Page number (left) -->
    <xsl:template match="tei:fw[@rend='left']">
        <div class="fw left">
            <xsl:value-of select="."/>
        </div>
    </xsl:template>

    <!-- Centered header -->
    <xsl:template match="tei:fw[@rend='center']">
        <div class="fw center">
            <xsl:value-of select="."/>
        </div>
    </xsl:template>

    <!-- paragraphs -->
    <xsl:template match="tei:p">
        <p class="body-p">
            <xsl:apply-templates/>
        </p>
    </xsl:template>

    <!--inline elements (persName, placeName, date) -->
    <xsl:template match="tei:persName | tei:placeName | tei:date">
        <span class="{local-name()}">
            <xsl:apply-templates/>
        </span>
    </xsl:template>

    <!-- catch-all for text -->
    <xsl:template match="text()">
        <xsl:value-of select="."/>
    </xsl:template>
</xsl:stylesheet>
